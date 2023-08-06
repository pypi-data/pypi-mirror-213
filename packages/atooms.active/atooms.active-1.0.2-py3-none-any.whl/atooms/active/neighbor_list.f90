module neighbor_list
  implicit none

contains

  pure subroutine pbc(r,box,hbox)
    double precision, intent(inout) :: r(:)
    double precision, intent(in)    :: box(:), hbox(:)
    where (abs(r) > hbox)
       r = r - sign(box,r)
    end where
  end subroutine pbc

  pure subroutine distance(i,j,pos,rij)
    integer, intent(in) :: i, j
    double precision, intent(in)    :: pos(:,:)
    double precision, intent(inout) :: rij(:)
    rij = pos(:,i) - pos(:,j)
  end subroutine distance

  pure subroutine dot(r1,r2,out)
    double precision, intent(in)  :: r1(:), r2(:)
    double precision, intent(out) :: out
    out = dot_product(r1,r2)
  end subroutine dot

  subroutine zero(x)
    double precision, intent(inout)  :: x(:,:)
    x = 0.d0
  end subroutine zero

  subroutine compute(box,pos,ids,rcut,neighbors,number_neighbors,error)
    !! Compute neighbor lists using III Newton law
    double precision, intent(in)    :: box(:)
    double precision, intent(in)    :: pos(:,:), rcut  !(:,:)
    integer,          intent(in)    :: ids(:)
    integer,          intent(inout) :: neighbors(:,:), number_neighbors(size(pos,2))
    logical,          intent(out)   :: error
    double precision                :: rij(size(pos,1)), rijsq, hbox(size(pos,1))
    integer                         :: i, j, isp, jsp
    error = .false.
    
    ! box                 : box size
    ! pos                 : particle positions
    ! rcut                : cutoff radius
    ! ids                 : chemical species of particles
    ! neighbors           : neighbors indexes for each particle; 
    !                       see 'number_neighbors' for number of 
    !                       adjacent particles to particle of index i 
    ! number_neighbors    : number of neighbors for each particle
    ! error               : error flag
    
    hbox = box / 2

    do i = 1,size(pos,2)
       number_neighbors(i) = 0
       isp = ids(i)
       
       !add particle itself to its own neighs
       number_neighbors(i) = number_neighbors(i) + 1
       neighbors(number_neighbors(i),i) = i

       !do j = i+1,size(pos,2)
       do j = 1,size(pos,2)
          if (i==j) cycle
          jsp = ids(j)
          call distance(i,j,pos,rij)
          call pbc(rij,box,hbox)
          call dot(rij,rij,rijsq)
          ! print*, rijsq**0.5, rijsq <= rcut**2, i, j
          if (rijsq <= rcut**2) then
             number_neighbors(i) = number_neighbors(i) + 1
             if (number_neighbors(i) <= size(neighbors,1)) then
                neighbors(number_neighbors(i),i) = j
             else
                error = .true.
             end if
          end if
       end do
    end do
  end subroutine compute

end module neighbor_list
